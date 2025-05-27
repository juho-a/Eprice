import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { fail } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";

const datesInOrder = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    return start < end;
     
}

const getFormattedData = (data) => {
    const datetimesUTC = data.map(item => item.startTime);
    const datetimesHelsinki = datetimesUTC.map(dt =>
            new Date(dt).toLocaleString("fi-FI", { timeZone: "Europe/Helsinki" }));
    const productionValues = data.map(item => item.value);
    
    // sort the data by startTime in ascending order
    const sortedData = data.map((item, index) => ({
        startTime: datetimesUTC[index],
        productionValue: productionValues[index]
    })).sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
    
    return {
        "values": productionValues,
        "labels": datetimesHelsinki
    };
}

export const actions = {
  getProductionRange: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/production/range`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
         },
        body: JSON.stringify(data)
      });

      if (!res.ok) {
        return fail(res.status, { error: "API refusing to serve data..." });
      }

      const productionData = await res.json();
      const { values, labels } = getFormattedData(productionData);
      return { 
        productionValues: values,
        productionLabels: labels,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  },

  getConsumptionRange: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/consumption/range`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
         },
        body: JSON.stringify(data)
      });

      if (!res.ok) {
        return fail(res.status, { error: "API refusing to serve data..." });
      }

      const consumptionData = await res.json();
      const { values, labels } = getFormattedData(consumptionData);
      return { 
        consumptionValues: values,
        consumptionLabels: labels,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  }
  
};