import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
const baseURL = 'http://localhost:8000'

Vue.use(Vuex)

export const state = {
  results: Array,
  drugs: Array,
  symptoms: Array,
}

export const mutations = {
    updateResults(state, {newResults}) {
        state.results = newResults
    },
    updateDrugs(state, {newDrugs}) {
        state.drugs = newDrugs
    },
    updateSymptoms(state, {newSymptoms}) {
        state.symptoms = newSymptoms
    }
}

export const actions = {
    fetchResults({commit}, {searchType, searchTerm, symptoms}) {
        let params
        if(searchType=="query"){
            params = {searchType, searchTerm}
        }
        else if(searchType=="checkBox"){
            params = {searchType, symptoms}
        }
        return axios.post(baseURL + '/search', params)
            .then((resp) => {
                commit('updateResults', {newResults: resp.data})
                // debugger
            })
    },
    fetchDrugs({commit}, {getAllDrugs, drugs, fetchingMethod}) {
        // fetchMethod: "ID", "name", "type"
        return axios.post(baseURL + '/getDrugs',{getAllDrugs, drugs, fetchingMethod})
            .then((resp) => {
                commit('updateDrugs', {newDrugs: resp.data})
                // debugger
            })
    },
    fetchSymptoms({commit}, {getAllSymptoms, symptoms, fetchingMethod}) {
        return axios.post(baseURL + '/getSymptoms',{getAllSymptoms, symptoms, fetchingMethod})
            .then((resp) => {
                commit('updateSymptoms', {newSymptoms: resp.data})
                // debugger
            })
    }
}

const store = new Vuex.Store({
  state,
  actions,
  mutations
})

export default store
