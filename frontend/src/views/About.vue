<template>
  <div class="about">
    <div class="text">
      <p></p><b>Ask Marley</b> is a search engine which was developed for the final project of the web information
      retrieval course in Tsinghua University in the spring semester 2018-2019 by André Cavalheiro. </p>
      <p> The main aim of this project is to provide further information on illicit drugs to anyone interested in the topic.
      The principal focus during the development of this platform was to filter between all drugs according to the symptoms
      each substance provides.</p>
      <p> The information present here was gathered by crawling the web, mainly sites who seemed the most trustworthy and who
      allowed their information to be collected. The list of crawled sites can be seen in the source code of the project under
        the spider directory which can be found <a href="https://github.com/andre-cavalheiro/ask-marley">here</a></p>
      <p>Special thanks to David Norte for providing the platform name </p>
      <br><br>
    </div>
    <div class="footer">
        <small>
          <b><p>Powered with ❤ by: </p></b>
          <p>Vue.js</p>
          <p>MongoDB</p>
          <p>Scrappy - web crawler</p>
          <p>Falcon - web framework</p>

        </small>
    </div>
  </div>
</template>


<style>
  .text {
    text-align: justify;
    text-justify: inter-word;
    padding-left: 10%;
    padding-right: 10%;
  }
  .footer {
    font-size: 80%;
    line-height: 6px;
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
  }

</style>
