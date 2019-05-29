<template>
  <div class="result-entry-container">
    <router-link :to="{ name: 'drugInfo', params: {drug}}">
      <h3>{{capitalize(drug.commonName)}}</h3>
    </router-link>

    <p><small>Matched {{drug.symptomsMatched}} symptoms</small></p>

    <b>Other names: </b>
      <p class="drug-names" v-for="name in drug.otherNames">{{capitalize(name)}}; </p>
      <br><br>
    <b>First description: </b>
    {{capitalize(drug.description[0])}}
  </div>
</template>

<script>
export default {
  name: 'single-result',
  props: {
    drug: {
      required: true,
      type: Object
    },
  },
  methods: {
    capitalize: (s) => {
      if (typeof s !== 'string') return ''
      return s.charAt(0).toUpperCase() + s.slice(1)
    }
  }

}
</script>


<style>
  .result-entry-container {
    text-align: justify;
    text-justify: inter-word;
  }

</style>