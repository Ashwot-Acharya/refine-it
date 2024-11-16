import React, { useState , useEffect} from 'react';
import ProjectLIst from './components/ProjectLIst';
import  SideBar from './components/SideBar'



function Dashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:3000/projects'); // Replace 'items' with your endpoint
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

return(<div>
      
      <SideBar />
      
      <br /><br /><br />
      
      <ProjectLIst pjcts={data}/>

      
      

    </div>

  );
}

export default Dashboard