import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

import './Homepage.css'
import man from './man.png'

function Homepage() {
  return (
    <Container fluid className="homeContainer">
      <Row>
        <Col className="image">
          <img src={man} alt="/"/>
        </Col>
        <Col>
        <div className="paragraph">
          <h1>We can help you!</h1>
          <h1>Find your matching job!</h1>
        <h5>Here is where the dream start</h5>
        <Button href="/register" variant="primary" size="lg">
        Join Now
      </Button>
        </div>
        </Col>
      </Row>
    </Container>
  );
};
  
export default Homepage;