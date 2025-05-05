import { browser } from "$app/environment";
import * as dataApi from "$lib/apis/data-api.js";

let pricesState = $state({});

if (browser) {
  pricesState = await dataApi.readPublicData();
}

const usePricesState = () => {
  return {
    get data() {
      return pricesState;
    },
    update: async () => {
      pricesState = await dataApi.readPublicData();
    },
    // this is a trick for chart.js to get the data
    // it needs to be a plain object
    // otherwise it will not work
    state2js: () => {
      const temp = JSON.stringify(pricesState);
      return JSON.parse(temp);
    },
  }
};

export { usePricesState };