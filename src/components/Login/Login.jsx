import React from "react";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import './Login.css'

function Login() {
  return (
    <Container className="loginForm">
    <h1>Sign into your account</h1>
    <Form>
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
          <Button type="submit" value="applicant">Log In As Applicant</Button>
        </Col>
        <Col  className="rightBtn">
          <Button type="submit" value="company">Log In As Company</Button>
        </Col>
      </Form.Group>
    </Form>
    <p>Don't have an account? &nbsp; <a href="/register">Register here</a></p>
    </Container>
  );
}
  
export default Login;