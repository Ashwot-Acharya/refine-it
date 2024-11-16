import React from 'react'

function RefRec(wts) {
    const dpair=wts.data

    const peps=dpair[0];
    const collection =[];
    for(const pid in peps){
        collection.push(peps[pid]);
    }

  return (

    <div className=" p-6 bg-gray-100 h-1/4 w-1/2">
      <h1 className="text-2xl font-bold mb-4 border-t-5 border-gray">{dpair[1]}</h1>
      <ul className="space-y-4 pl-5 list-disc" >
        {
            collection.map((peps) =>(
              <div>
                              
                   <li><a href="" className='text-gray-600 hover:text-blue-500'>{peps["Title"]} - {peps["Authors"]}</a></li>             
              
                  
      <br /><br />
      </div>
            ))
        }
    </ul>
    </div>
  )
}

export default RefRec