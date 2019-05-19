<template>
  <div class="container">
    <div class="result-list" align="left">
      <SingleDrug
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