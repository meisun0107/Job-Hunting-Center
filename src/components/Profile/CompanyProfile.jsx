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
import { useState, useEffect } from "react";

import { Auth } from "aws-amplify";

function CompanyProfile() {
  const [user, setUser] = useState(null);

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

  console.log(user);
  if (!user) {
    return <div>Loading...</div>;
  }
  

  function sendData(event) {
    event.preventDefault(); // prevent the form from submitting
    const title = event.target.elements.formHorizontalTitle.value;
    const description = event.target.elements.formHorizontalDescription.value;
    const data = {"email":"123test@gmail.com", "position_name": title, "position_description": description};

    var additionalParams = {
			headers: {
				"Content-Type": "multipart/form-data",
			}, 
      params: {
        email:user.attributes.email, 
        position_name: title, 
        position_description: description
      }
		};

    console.log(data.type)
    axios.post("https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/postposition", data, additionalParams).then((response) => {
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
        <p>Email: {user.attributes.email}</p>
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