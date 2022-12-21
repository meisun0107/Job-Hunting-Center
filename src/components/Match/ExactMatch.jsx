import React, { useState, Component }from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';
import axios from "axios";
import './Match.css';

function ExactMatch() {

  const applyJob = (event) => {
    alert("This function is not available right now.")
  };
  return (
    <Container fluid className="matchContainer">
      <Row >
      <h4 className="jobs">Exact Match Result</h4>
      <Table striped className="jobTable">
      <thead>
        <tr>
          <th>Posted Job List</th>
          <th>Match Percent</th>
          <th>Click here to apply</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>job 1</td>
          <td>97%</td>
          <td><button>Apply</button></td>
        </tr>
        <tr>
          <td>job 2</td>
          <td>90%</td>
          <td><button onClick={applyJob}>Apply</button></td>
        </tr>
      </tbody>
    </Table>
      </Row>
    </Container>
  );
};
  
export default ExactMatch;