import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { fail } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";

const datesInOrder = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    return start < end;
};

const getFormattedData = (data) => {
    const datetimesUTC = data.map(item => item.startTime);
    const datetimesHelsinki = datetimesUTC.map(dt =>
        new Date(dt).toLocaleString("fi-FI", {
            timeZone: "Europe/Helsinki",
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit"
            // no 'second'
        })
    );
    const values = data.map(item => item.value);

    // Sort by startTime just in case
    const sorted = data
        .map((item, index) => ({
            startTime: datetimesHelsinki[index],
            value: values[index]
        }))
        .sort((a, b) => new Date(a.startTime) - new Date(b.startTime));

    return {
        values: sorted.map(item => item.value),
        labels: sorted.map(item => item.startTime)
    };
};

export const actions = {
    getCombinedRange: async ({ request, cookies }) => {
        const fdata = await request.formData();
        const data = Object.fromEntries(fdata);

        if (!data.startTime || !data.endTime) {
            return fail(400, { error: "Start and end dates are required." });
        } else if (!datesInOrder(data.startTime, data.endTime)) {
            return fail(400, { error: "Start date must be before end date." });
        }

        try {
            // Fetch both datasets in parallel
            const [prodRes, consRes] = await Promise.all([
                fetch(`${PUBLIC_INTERNAL_API_URL}/api/production/range`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
                    },
                    body: JSON.stringify(data)
                }),
                fetch(`${PUBLIC_INTERNAL_API_URL}/api/consumption/range`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
                    },
                    body: JSON.stringify(data)
                })
            ]);

            if (!prodRes.ok || !consRes.ok) {
                return fail(500, { error: "API refusing to serve data..." });
            }

            const productionData = await prodRes.json();
            const consumptionData = await consRes.json();

            // Format both datasets
            const prodFormatted = getFormattedData(productionData);
            const consFormatted = getFormattedData(consumptionData);

            // Use the longer label array for the x-axis
            const labels =
                prodFormatted.labels.length >= consFormatted.labels.length
                    ? prodFormatted.labels
                    : consFormatted.labels;

            let productionValues = prodFormatted.values;
            let consumptionValues = consFormatted.values;
            let differenceValues = [];

            const meanProduction = productionValues.reduce((sum, val) => sum + val, 0) / productionValues.length;
            const meanConsumption = consumptionValues.reduce((sum, val) => sum + val, 0) / consumptionValues.length;
            const meanDifference = meanProduction - meanConsumption;

            differenceValues = productionValues.map((val, i) => val - (consumptionValues[i] ?? 0));
            return {
                labels,
                productionValues: data.selection === "production" || data.selection === "both" ? productionValues : [],
                consumptionValues: data.selection === "consumption" || data.selection === "both" ? consumptionValues : [],
                differenceValues,
                meanProduction,
                meanConsumption,
                meanDifference,
                startTime: data.startTime,
                endTime: data.endTime,
                selection: data.selection
            };
            
        } catch (e) {
            return fail(500, { error: "Server error" });
        }
    }
};