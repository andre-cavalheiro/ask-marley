<template>
  <div class="container">
    <h2>🇩​🇷​🇺​🇬​ 🇧​🇦​🇳​🇰​</h2>
    <div>
      <ul class="drug-names-up">
        <li
            v-for="(drug, index) in drugs"
            :key="index">
          <a :href="'#'+drug.commonName">{{capitalize(drug.commonName)}}</a>
        </li>
      </ul>
    </div>
    <div class="drug-list" align="left">
      <SingleDrug
              class="boxed"
              v-for="(drug, index) in drugs"
              :key="index"
              :drug="drug"
      />
    </div>
  </div>
</template>

<script>
  import SingleDrug from '@/components/SingleDrug.vue'

  export default {
    name: 'drugs',
    props: {
      fetchAll: {
        required: false,
        type: Boolean
      },
    },
    methods: {
      capitalize: (s) => {
        if (typeof s !== 'string') return ''
        return s.charAt(0).toUpperCase() + s.slice(1)
      }
    },
    computed: {
      drugs() {
        return this.$store.state.drugs
      },
    },
    components: {
      SingleDrug
    },
    mounted() {
      if(this.fetchAll){
        this.$store.dispatch('fetchDrugs', {getAllDrugs: true})
      }
    }
  }
</script>

<style>
  .drug-names-up{
    -webkit-column-count: 6; /* Chrome, Safari, Opera */
    -moz-column-count: 6; /* Firefox */
    column-count: 6;

    display: inline-block;
    list-style-type: none;
    border: 1px solid black ;
    margin: 7%;
    text-align: justify;
    text-justify: inter-word;
    padding: 1%;
  }

</style>