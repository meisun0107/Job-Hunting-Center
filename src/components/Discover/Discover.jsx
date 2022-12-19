import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import './Discover.css'
  
function Discover() {
  return (
    <div>
      <Container className="discover">
      <Row>
        <Col className="content">

          <h1>Our System is where you can find the jobs that match you the most.</h1>
        <p>People are always eager to find the job which match their skills most. 
JRC is the right place. We provide the service to help you with your career. 
We can match you with the most related careers so that help you win easier in your career path.
We have helped thoudsands of people who were suffering from get the information about their paired jobs. 
So trust us, and give us an opportunity. We won’t let you down!</p>
<p>Contact: (646)-925-9433 &nbsp; &nbsp; &nbsp; Instagram: jobrecommendercenter_</p>
        </Col>
      </Row>
    </Container>
    </div>
  );
};
  
export default Discover;