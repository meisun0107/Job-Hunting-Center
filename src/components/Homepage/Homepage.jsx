import React, {useEffect, useState} from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

import './Homepage.css'
import man from './man.png'
import { Auth } from 'aws-amplify';
import axios from 'axios';
function Homepage() {
  const [user, setUser] = useState(null);
  const [tag, setTag] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        const user = await Auth.currentAuthenticatedUser();
        setUser(user);
        const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
        axios.get(url, {
          params: {
            email: user.attributes.email,
          }
        }).then((response) => {
          setTag(response.data.user_tag);
          console.log(response.data);
        });
      } catch (error) {
        console.log(error);
      }
    }
    fetchUser();
  }, []);

  if (!user) {
    return <div>Loading...</div>;
  }

  console.log(user);



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
        <Button href="/company-profile" variant="primary" size="lg">
        Post a job as a company!
      </Button> 
      <p></p>
       <Button href="/user-profile" variant="primary" size="lg">
        View my profile and start matching!
      </Button>
        </div>
        </Col>
      </Row>
    </Container>
  );
};
  
export default Homepage;