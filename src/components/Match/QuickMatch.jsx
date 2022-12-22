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

  const url = "PATH-TO-QUICK-MATCH";
  axios.get(url, {
    params: {
      email: user.attributes.email
    }
  }).then((response) => {
    console.log(response.data);
  });

  const applyJob = (event) => {
    alert("This function is not available right now.")
  };

  return (
    <Container fluid className="matchContainer">
      <Row >
      <h4 className="jobs">Cluster Match Percent: 83%</h4>
      <Table striped className="jobTable">
      <thead>
        <tr>
          <th>Jobs in this cluster</th>
          <th>Click here to apply</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>job 1</td>
          <td><button onClick={applyJob}>Apply</button></td>
        </tr>
        <tr>
          <td>job 2</td>
          <td><button onClick={applyJob}>Apply</button></td>
        </tr>
      </tbody>
    </Table>
      </Row>
    </Container>
  );
};
  
export default QuickMatch;