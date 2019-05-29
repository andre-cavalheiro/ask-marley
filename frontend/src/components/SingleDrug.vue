<template>
  <div class="result-entry-container">
    <h2 :id="drug.commonName">{{capitalize(drug.commonName)}}</h2>
    <b>Drug types: </b> <p class="drug-type" v-for="type in drug.types">{{capitalize(type)}}; </p>
    <br><br>
    <br><br>
    <b>Other names: </b>
    <p class="drug-names" v-for="name in drug.otherNames">{{capitalize(name)}}; </p>
    <br><br>
    <b>Information</b>
    <p class="drug-info" v-for="info in drug.description">{{capitalize(info)}}</p>
    <br><br>
    <b>Risks</b>
    <p v-for="risk in drug.risks">{{capitalize(risk)}}</p>
  </div>
</template>

<script>
export default {
  name: 'single-drug',
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
    border: 1px solid black ;
    outline:1px solid black;
    padding-top: 20px;
    padding-right: 30px;
    padding-bottom: 50px;
    padding-left: 80px;
  }
  .drug-type, .drug-names {
    display:inline;
  }

</style>