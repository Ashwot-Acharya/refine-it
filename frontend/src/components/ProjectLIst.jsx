import React from "react";
import { useState,useEffect } from "react";
import  ReactModal from 'react-modal';
import RefRec from "./RefRec";








function ProjectLIst(prfd) {

  const [isOpen,setIsOpen]=useState(false);
  const togglePopup = () => setIsOpen(!isOpen);
  const data = prfd.pjcts;

 
  const [expandedRows, setExpandedRows] = useState({});

  const toggleRow = (id) => {
      


    setExpandedRows((prev) => ({
      
      [id]: !prev[id],
    }));
  };

  return (
    <div className="">
      <button
       onClick={togglePopup}
       className='bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded float-right py-auto'
  >
       New Paper
     </button>
     
     <ReactModal
           isOpen={isOpen}
           onRequestClose={togglePopup}
           style={{ overlay: { backgroundColor: 'rgba(0, 0, 0, 0.5)' } }}
           className='mx-auto my-9 p-9 w-1/3 h-1/3'
         >
           <form className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 '>
             <label className='block text-gray-700 text-sm font-bold mb-2'>Title</label>
             <input type="text" className='shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline w-full' />
             <label className='block text-gray-700 text-sm font-bold mb-2'> Your Document</label>
 
             <div class="flex items-center justify-center w-full">
     <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
         <div class="flex flex-col items-center justify-center pt-5 pb-6">
             <svg class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                 <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
             </svg>
             <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
             <p class="text-xs text-gray-500 dark:text-gray-400">DOC. DOCX.</p>
         </div>
         <input id="dropzone-file" type="file" class="hidden" />
     </label>
 </div> 
             
             <br />
             <button type="submit" className='bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex justify-center'>Analyze and Upload</button>
           </form>
         </ReactModal>
        <h1 className="text-5xl font-serif">
            

        </h1>
        <br /><br />
        <div className="Plist">
     



    <table className="table-auto w-full text-xl text-left rtl:text-right text-black-100 dark:text-black-400 font-mono">
      <thead className="dark:bg-gray-400 dark:text-black-400">
        <tr>
          <th className="px-6 py-3">Name</th>
          <th className="px-6 py-3">Upload Date</th>
          <th className="px-6 py-3">Original Document</th>
          <th className="px-6 py-3">Document With Citation Added</th>
          <th className="px-6 py-3"></th>

        </tr>
      </thead>
      <tbody>
        {data.map((project) => (
          <React.Fragment key={project.id}>
            {/* Main Row */}
            <tr className="odd:bg-white odd:dark:bg-gray-200 even:bg-gray-50 even:dark:bg-gray-50 border-b dark:border-gray-50">
              <td className="px-6 py-4">{project.project_name}</td>
              <td className="px-6 py-4">{project.upload_date}</td>
              <td className="px-6 py-4">
                <button className="bg-blue-500 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded">
                  <svg
                    viewBox="0 0 21 21"
                    fill="currentColor"
                    height="1em"
                    width="1em"
                  >
                    <g
                      fill="none"
                      fillRule="evenodd"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M8.5 3.5H6.498a2 2 0 00-2 2v10a2 2 0 002 2h8c1.104 0 2-.896 2-2l.002-8-4-4" />
                      <path d="M13.5 10.586l-3 2.914-3-2.914M10.5 2.5v11" />
                    </g>
                  </svg>
                </button>
              </td>


              <td className="px-6 py-4">
                <button className="bg-green-500 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded">
                  <svg
                    viewBox="0 0 21 21"
                    fill="currentColor"
                    height="1em"
                    width="1em"
                  >
                    <g
                      fill="none"
                      fillRule="evenodd"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M8.5 3.5H6.498a2 2 0 00-2 2v10a2 2 0 002 2h8c1.104 0 2-.896 2-2l.002-8-4-4" />
                      <path d="M13.5 10.586l-3 2.914-3-2.914M10.5 2.5v11" />
                    </g>
                  </svg>
                </button>
              </td>

              <td className="px-6 py-4">
                <button
                  onClick={() => toggleRow(project.id)}
                  className="bg-blue-500 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded"
                >
                     <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="1em"
      width="1em"
    >
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h7c-.41-.25-.8-.56-1.14-.9a6.478 6.478 0 01-.36-9.18C13.69 9.5 17.33 9.13 20 11V8l-6-6m-1 7V3.5L18.5 9H13m7.31 9.9c1.33-2.11.69-4.9-1.4-6.22-2.11-1.33-4.91-.68-6.22 1.4-1.34 2.11-.69 4.89 1.4 6.22 1.46.93 3.32.93 4.79.02L22 23.39 23.39 22l-3.08-3.1m-3.81.1a2.5 2.5 0 01-2.5-2.5 2.5 2.5 0 012.5-2.5 2.5 2.5 0 012.5 2.5 2.5 2.5 0 01-2.5 2.5z" />
    </svg>
                </button>
              </td>
            </tr>

            {/* Expandable Row */}
            <tr
              className={`transition-all duration-300 ease-in-out ${
                expandedRows[project.id] ? 'max-h-screen' : 'max-h-0 overflow-hidden'
              }`}
            >
              <td colSpan="4" className="px-6 py-4 ">
                {expandedRows[project.id] && (
                  <div className="p-4 bg-gray-100 dark:bg-gray-300 rounded-lg text-sm ">
                    <h4 className=" font-semibold"></h4>
                    <div className="flex item-center justify-center divide-x-0 ">
                      <RefRec data={[project.refs,"Referenced Literature"]}/>
                      <RefRec data={[project.recs,"Similar Topics"] }/>
                      {/* <ProjectLibrary data={project.refs} />   
                      <Recommendations data={project.recs}/>                    */}
                    </div>

                  </div>
                )}
              </td>
            </tr>
          </React.Fragment>
        ))}
      </tbody>
    </table>
  


        </div>

    </div>
  )
}

export default ProjectLIst