<template>
  <div class="home">
    <!--<img alt="Vue logo" src="../assets/logo.png">-->
    <h2>🇸​🇪​🇦​🇷​🇨​🇭​ 🇸​🇾​🇲​🇵​🇹​🇴​🇲​🇸​</h2>
    <button class="myButtonNav" @click="changeSearchMethod(0)"> CheckBox </button>
    <button class="myButtonNav" @click="changeSearchMethod(1)"> Query </button>
    <br>
    <br>
    <div v-if="searchMethod == 0">
      <form @submit.prevent="performSearchByCheckBox">
        <button class="myButtonNav" type="submit">Search</button>


        <ul class="symptom-list">
              <div v-for="symptom in symptoms">
                <li class="symptom-checkbox">
                    <input type="checkbox" :id="symptom.ID" :value="symptom.commonName" v-model="checkedSymptoms">
                    <label :for="symptom.ID">{{capitalize(symptom.commonName)}}</label>
                </li>
              </div>
          </ul>

      </form>
    </div>  
    {{checkedSymptoms}}
    <div v-if="searchMethod == 1">
      <form @submit.prevent="performSearchByString">
        <input v-model="searchTerm" placeholder="Search your symptoms">
        <button class="myButtonNav" type="submit">Search</button>
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
import checkbox from 'vue-material-checkbox'

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
    Results,
    checkbox
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
    capitalize: (s) => {
      if (typeof s !== 'string') return ''
        return s.charAt(0).toUpperCase() + s.slice(1)
      }
  },
  mounted() {
    // this.$store.commit('updateResults', {"newResults":[]})
    this.$store.dispatch('fetchSymptoms', {getAllSymptoms: true})
  }
}
</script>

<style>
    /*.symptom-list li{
        display:inline-block;
        width:100%;
    }*/
    /*
    .symptom-list li{
        display: inline-grid;
        width: 20%;
        height: 100%;
        margin: 5px;
        border: 1px solid black ;
        padding: 3px;
    }*/
    .symptom-list{
        -webkit-column-count: 5; /* Chrome, Safari, Opera */
        -moz-column-count: 5; /* Firefox */
        column-count: 5;
    }
    .symptom-checkbox{
        list-style-type: none;
        border: solid black ;
        margin: 2%;
        text-align: justify;
        text-justify: inter-word;
        padding: 1%;
        /*padding-top: 2%;
        padding-right: 2%;
        padding-bottom: 2%;
        padding-left: 2%;
        */
    }

</style>

