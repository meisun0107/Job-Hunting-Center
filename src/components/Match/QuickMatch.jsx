import React, { useState }from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';
import axios from "axios";
import './Match.css';

function QuickMatch() {
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
          <td><button>Apply</button></td>
        </tr>
        <tr>
          <td>job 2</td>
          <td><button>Apply</button></td>
        </tr>
      </tbody>
    </Table>
      </Row>
    </Container>
  );
};
  
export default QuickMatch;