import React,{ Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
// import $ from 'jquery';
// import Popper from 'popper.js';
import 'bootstrap/dist/js/bootstrap.bundle.min';
const CryptoJS = require('crypto-js');




const encrypt = async (text) => {
    return await CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(text));
};
  
const decrypt = async (data) => {
    return await CryptoJS.enc.Base64.parse(data).toString(CryptoJS.enc.Utf8);
};


class Form extends Component{ 
constructor(props){ 
	super(props) 
	this.state = { email:'',password:''} 
	this.handleChange = this.handleChange.bind(this) 
	this.handleSubmit = this.handleSubmit.bind(this) 
} 


async handleSubmit(event){ 
    /**
     * Basic login logic 
     * 
     * will take event and from the event it will extract password and email and 
     * authenticate a user in the back end
     * 
     * 
     * @param event : object
     */
	const { email, password} = this.state 
	event.preventDefault()
    const BASE_URL = 'http://localhost:9100/api_root/auth/login/';


    let loginFormData = new FormData()

    
    loginFormData.append('username', email)
    loginFormData.append('password', password)
    loginFormData.append('grant_type', 'password')
    loginFormData.append('client_secret', 'ofNtIXksHfRWEdK1N7fWNioOM4ixojCHh3Gs6EzSdV6Z1eDXnvkdW0NSiz76Rupc4868oxccseCO5idQkxg4HMyWENtGONj3Zp1CUTvfjtQtClXJLEtRJV0uV3KYDM2n')
    loginFormData.append('client_id', 'ugD0Dt7DPC1D7HFhN0gPFjXslnFT5debJyu41bmj')


    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)

    console.log(bodyStr)
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: bodyStr 
    }

    const response = await fetch(BASE_URL, options);
    let res;

    if (response.ok){
        res = await response.json();
    } else {
        // error message form the backend
        const text = await response.text()
        // alert(text)
        console.log(text)
    }
    

    let handelStore = async (accessToken, refrasheToken) => {
        /**
         * encript the access and refrash token and store it in local storage
         * 
         * later on it will be changed to another place untile then it will be stord in localstorage
         * 
         * @param access_token : string 
         * @param refrash_token : string
         * 
         * @returns boolien
         */
        const encriptedAccessToken = await encrypt(accessToken);
        const encriptedRefrashToken = await encrypt(refrasheToken);
        localStorage.setItem('access_token', encriptedAccessToken);
        localStorage.setItem('refrash_token', encriptedRefrashToken);
        return true;
    }
    
    if (res) {
        let out = await handelStore(res.access_token, res.refresh_token);
        if(out) {
            // do something
        }
    } else {
        // TODO: handel login errors elegantly
        alert('something went wrong')
    }
	
} 

handleChange(event){ 
	this.setState({
	[event.target.name] : event.target.value 
	}) 
} 

render(){ 
	return( 
    <div className='card'>
        <div className=' card-header'>Login</div>
        <div className='card-body'>
            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label htmlFor='email'>Email or User Name</label> 
                    <input id='email' type='text' className=' form-control' name='email' placeholder='Email or User Name' value = {this.state.email} onChange={this.handleChange} /> 
                </div> 
                <div className='form-group'> 
                    <label htmlFor='password'>Password</label> 
                    <input id='password' name='password' className='form-control' placeholder='password' value={this.state.password} onChange={this.handleChange} /> 
                </div>
                <button className='btn btn-danger'>Login</button>
            </form>
        </div>
    </div>
	) 
} 
} 

export default Form;