import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from "axios";
import { useState, useEffect } from "react";

import { Auth } from "aws-amplify";

import './EditInfo.css';

function EditInfo() {
  const [user, setUser] = useState(null);
  const [mytag, setTag] = useState(null);
  const [username, setUsername] = useState(null);

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
  const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
  axios.get(url, {
    params: {
      email: user.attributes.email
    }
  }).then((response) => {
    setTag(response.data.user_tag);
    setUsername(response.data.username);
    console.log(mytag);
  });
  

  function sendData(event) {
    event.preventDefault(); // prevent the form from submitting
    const username = event.target.elements.formHorizontalTitle.value;
    const tag = event.target.elements.formHorizontalTag.value;
    const data = {"email": user.attributes.email, "position_name": username, "user_tag": tag};

    var additionalParams = {
			headers: {
				"Content-Type": "multipart/form-data",
			}, 
      params: {
        email: user.attributes.email, 
        username: username,
        user_tag: tag,
      }
		};

    const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
    axios.post(url, data, additionalParams).then((response) => {
      console.log(response.data);
      alert("you have successfully updated your profile!");
    });
  }

  return (
    <Container>
      <Row>
        <Col className="editContainer">
        <Form action="" method="POST" onSubmit={sendData}>
      <Form.Group as={Row} className="mb-3" controlId="formHorizontalTitle">
        <Col sm={10}>
          <Form.Control type="text" placeholder="Username / Company Name" defaultValue={username}/>
        </Col>
      </Form.Group>
      <Form.Group as={Row} className="mb-3" controlId="formHorizontalTag" >
        <Col sm={10}>
          <Form.Control type="text" placeholder="are you a company or an user? (please only type company or user)" defaultValue={mytag}/>
        </Col>
      </Form.Group>

      <Form.Group as={Row} className="mb-3">
        <Col className="postBtn">
          <Button type="submit">Update</Button>
        </Col>
      </Form.Group>
    </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default EditInfo;