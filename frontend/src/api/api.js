import axios from 'axios'

const baseURL = 'http://localhost:8000'

async function fetchResults(searchTerm) {

  // const response = await client.get('/search', { params: { searchTerm } })
  return axios.get(baseURL + '/search')
  // return response.data
  // return new Promise(()=>("at least it's running"))
}


export default {
  fetchResults
}
