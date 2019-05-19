<template>
  <div class="home">
    <!--<img alt="Vue logo" src="../assets/logo.png">-->
    <h1>What you're feeling ?</h1>
    <button @click="changeSearchMethod(0)"> CheckBox </button>
    <button @click="changeSearchMethod(1)"> Query </button>
    <br>
    <br>
    <div v-if="searchMethod == 0">
      <form @submit.prevent="performSearchByCheckBox">
        <div v-for="symptom in symptoms">
          <input type="checkbox" :id="symptom.ID" :value="symptom.commonName" v-model="checkedSymptoms">
          <label :for="symptom.ID">{{symptom.commonName}}</label>
        </div>
        <!--
        <input type="checkbox" id="hallucinating" value="hallucinating" v-model="checkedSymptoms">
        <label for="hallucinating">Hallucinating</label>
        -->
        <button type="submit">Submit</button>
      </form>
    </div>
    {{checkedSymptoms}}
    <div v-if="searchMethod == 1">
      <form @submit.prevent="performSearchByString">
        <input v-model="searchTerm" placeholder="Search your symptoms">
        <button type="submit">Submit</button>
      </form>
    </div>
    <br>
    <br>
    <!--
    <br>
    <p>{{searchTerm}}</p>
    <span>{{ checkedSymptoms }}</span>
    -->
    <Results/>
  </div>
</template>

<script>
import Results from '@/views/Results.vue'

export default {
  name: 'home',
  data: () => {
    return {
      searchMethod: 0,
      searchTerm: "",
      checkedSymptoms: [],
    }
  },
  computed: {
    symptoms() {
      return this.$store.state.symptoms
    },
  },
  components: {
    Results
  },
  methods: {
    changeSearchMethod(newSearchMethod) {
      this.searchMethod = newSearchMethod
    },
    async performSearchByString() {
      this.$store.dispatch('fetchResults', {searchType: "query", searchTerm: this.searchTerm})
    },
    async performSearchByCheckBox() {
      let symptomsIDs = this.symptoms.map((s) => {
        if(this.checkedSymptoms.includes(s.commonName)){
          return s.ID
        }
      })

      symptomsIDs = symptomsIDs.filter((id)=>{
        return id != undefined
      })
      this.$store.dispatch('fetchResults', {searchType: "checkBox", symptoms: symptomsIDs})
    },
  },
  mounted() {
    // this.$store.commit('updateResults', {"newResults":[]})
    this.$store.dispatch('fetchSymptoms', {getAllSymptoms: true})
  }
}
</script>
