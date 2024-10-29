import axios from 'axios'
const SERVER = 'http://127.0.0.1:5000'

// testing 
export function test(){
    return axios(SERVER + '/test')
}

export function register(){
    return axios.post(SERVER + '/register')
}