import axios from "axios";


const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 5000,
  headers: {
    // your headers here
  }
});

export default api;
