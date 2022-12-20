import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Table from 'react-bootstrap/Table';
import './Profile.css'
import company from './company.png'
import axios from "axios";

function CompanyProfile() {
  function sendData(event) {
    event.preventDefault(); // prevent the form from submitting
    const title = event.target.elements.formHorizontalTitle.value;
    const description = event.target.elements.formHorizontalDescription.value;
    const data = {title, description};

    console.log(data)
    axios.post("https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/postposition", data).then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }
  return (
    <Container fluid className="companyContainer">
      <Row>
        <Col sm={3} className="avatar">
          <img src={company} alt="/"/>
        </Col>
        <Col sm={3}>
        <div className="info">
        <p>Company: Job Hunting Center</p>
        <p>Email: jhc@gmail.com</p>
        </div>
        </Col>
        <Col sm={6} className="userBtns">
        <Form action="" method="POST" onSubmit={sendData}>
      <Form.Group as={Row} className="mb-3" controlId="formHorizontalTitle">
        <Col sm={10}>
          <Form.Control type="text" placeholder="Job Title" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} className="mb-3" controlId="formHorizontalDescription">
        <Col sm={10}>
          <Form.Control as="textarea" placeholder="What is this job about..." />
        </Col>
      </Form.Group>

      <Form.Group as={Row} className="mb-3">
        <Col className="postBtn">
          <Button type="submit">Post a new position</Button>
        </Col>
      </Form.Group>
    </Form>
        </Col>
      </Row>

      <Row >
      <h4 className="jobList">Posted Job List</h4>
      <Table striped className="jobTable">
      <thead>
        <tr>
          <th>#</th>
          <th>Job Title</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>job 1</td>
        </tr>
        <tr>
          <td>2</td>
          <td>job 2</td>
        </tr>
      </tbody>
    </Table>
      </Row>
    </Container>
  );
};
  
export default CompanyProfile;