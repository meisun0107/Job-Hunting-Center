import React from "react";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import './Register.css'
import axios from 'axios';

function Register() {
  const state = {
    button: 1
  };
  function sendData(event) {
    event.preventDefault(); // prevent the form from submitting
    const email = event.target.elements.formHorizontalEmail.value;
    const username = event.target.elements.formHorizontalUsername.value;
    const password = event.target.elements.formHorizontalPassword.value;
    var identity = "";
    if (state.button === 1) {
      identity = "applicant";
    }
    if (state.button === 2) {
      identity = "company";
    }
  
    const data = { email, username, password, identity};

    console.log(event)
    axios.post(" https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/v1/signup", data).then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <Container className="registerForm">
    <h2>JOIN US NOW!</h2>
    <h2>LET US PROVIDE YOU THE BEST SERVICE!</h2>
    <Form action="" method="POST" onSubmit={sendData}>
      <Form.Group as={Row} className="mb-3" controlId="formHorizontalUsername">
        <Form.Label column sm={2}>
          Username
        </Form.Label>
        <Col sm={10}>
          <Form.Control type="text" placeholder="Username / Company Name" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} className="mb-3" controlId="formHorizontalEmail">
        <Form.Label column sm={2}>
          Email
        </Form.Label>
        <Col sm={10}>
          <Form.Control type="email" placeholder="Email" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} className="mb-3" controlId="formHorizontalPassword">
        <Form.Label column sm={2}>
          Password
        </Form.Label>
        <Col sm={10}>
          <Form.Control type="password" placeholder="Password" />
        </Col>
      </Form.Group>
      

      <Form.Group as={Row} className="mb-3">
        <Col  className="leftBtn">
          <Button type="submit" value="applicant" name="identity" onClick={() => (state.button = 1)}>Register As Applicant</Button>
        </Col>
        <Col  className="rightBtn">
          <Button type="submit" value="company" name="identity" onClick={() => (state.button = 2)}>Register As Company</Button>
        </Col>
      </Form.Group>
    </Form>
    <p>Already have an account? &nbsp; <a href="/login">Login here</a></p>
    </Container>
    
  );
}
  
export default Register;