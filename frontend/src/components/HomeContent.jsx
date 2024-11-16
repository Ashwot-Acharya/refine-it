import React from 'react'
import sic from '/sic.png'
import  ReactModal from 'react-modal';
import { useState,useEffect } from "react";
function HomeContent() {

  const [isOpen,setIsOpen]=useState(false);
  const togglePopup = () => setIsOpen(!isOpen);
  return (
    <div className="content p-4">
    <div className="container">
      <div className="info">
        <h1>Welcome To   
          <b>  RefineIT</b>
          </h1>
          <br /><br />
      <p className='text-xl'>Transform the way you manage 
        research & references</p>            
        
        
        
        <button onClick={togglePopup}>Create a Free Account</button>
        <ReactModal
           isOpen={isOpen}
           onRequestClose={togglePopup}
           style={{ overlay: { backgroundColor: 'rgba(0, 0, 0, 0.5)' } }}
           className='mx-auto my-9 p-9 w-1/3 h-1/3'
         >
           <form className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 ' action='/signup'>
           <label className='block text-gray-700 text-sm font-bold mb-2'>Name</label>
             <input type="text" className='shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline w-full' />
             <label className='block text-gray-700 text-sm font-bold mb-2'>Email</label>
             <input type="text" className='shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline w-full' />
             <label className='block text-gray-700 text-sm font-bold mb-2'> Password</label>
             <input type="text" className='shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline w-full' />
             <label className='block text-gray-700 text-sm font-bold mb-2'> Confirm Password</label>
             <input type="password" className='shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline w-full' />

             
             <br />
             <button type="submit" className='bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex justify-center'>SignUp</button>
           </form>
         </ReactModal>



      </div>
      <div className="image w-500">
        <img src={sic}></img>

      </div>
    </div>
  </div>
  )
}

export default HomeContent