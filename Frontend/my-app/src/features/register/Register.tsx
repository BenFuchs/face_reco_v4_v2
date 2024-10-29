import React, { useState } from 'react'
import { testAsync, selectRegister } from './registerSlice'
import { useAppDispatch, useAppSelector } from '../../app/hooks';

const Register = () => {
    const [username, setusername] = useState<string>('')
    const [password, setpassword] = useState<string>('')
    const [email, setemail] = useState<string>('')

    const dispatch = useAppDispatch();
    // const register = useAppSelector(selectRegister);

    const handleTestAsync = () => {
        dispatch(testAsync())
    }

  return (
    <div>
        <h1> Register  </h1>
        <label> Username: </label>
        <input type="text" onChange={(e)=>setusername(e.target.value)} value={username} id='username'/>   

        <label> Email: </label>
        <input type="text" onChange={(e)=>setemail(e.target.value)} value={email} id='email'/>   

        <label> Password: </label>
        <input type="text" onChange={(e)=>setpassword(e.target.value)} value={password} id='password'/>   


        <button onClick={handleTestAsync}>TEST</button>
    </div>
  )
}

export default Register