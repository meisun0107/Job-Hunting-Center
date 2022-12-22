import React, { useState, useEffect }from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';
import axios from "axios";
import './Match.css';
import { Auth } from 'aws-amplify';

function QuickMatch() {
  const [user, setUser] = useState(null);
  const [job, setJob] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        const user = await Auth.currentAuthenticatedUser();
        setUser(user);
      } catch (error) {
        console.log(error);
      }
    }

    fetchUser();
  }, []);

  if (!user) {
    return <div>Loading...</div>;
  }

  var jobs = [];
  const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/quickmatch";
  axios.get(url, {
    params: {
      email: user.attributes.email
    }
  }).then((response) => {
    console.log(response.data);
    
    for (let i = 0; i < response.data.length; i++) {
      jobs.push(<tr>
        <td>{response.data[i].positionid}</td>
        <td>{response.data[i].position_description}</td>
        <td>{response.data[i].company_email}</td>
        <td><button onClick={applyJob}>Apply</button></td>
      </tr>)
    }
    setJob(jobs);
  });

  const applyJob = (event) => {
    alert("This function is not available right now.")
  };

  return (
    <Container fluid className="matchContainer">
      <Row >
      <h4 className="jobs">Quick Match Result</h4>
      <Table striped className="jobTable">
      <thead>
        {<tr>
          <th>Jobs in this cluster</th>
          <th>Job Description</th>
          <th>Company Email</th>
          <th>Click here to apply</th>
        </tr>}
      </thead>
      <tbody>
        {job}
      </tbody>
    </Table>
      </Row>
    </Container>
  );
};
  
export default QuickMatch;