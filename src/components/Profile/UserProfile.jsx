import React, { useState, useEffect }from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Table from 'react-bootstrap/Table';

import './Profile.css'
import candidate from './candidate.png'
import axios from "axios";

import { Auth } from 'aws-amplify';

function UserProfile() {
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

  console.log(user)

  const [file, setFile] = useState()
  function handleChange(event) {
    setFile(event.target.files[0])
  }
  const uploadResume = (event) => {
    event.preventDefault(); // prevent the form from submitting

    console.log(file.type);
    const formData = new FormData();
    formData.append('file', file);
    
    var additionalParams = {
			headers: {
        "Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Headers": "*",
				"Access-Control-Allow-Methods": "PUT",
				"Content-Type": file.type,
			},
		};

    const puturl = "https://794k191dy4.execute-api.us-east-1.amazonaws.com/v1/upload/resume-of-jrc-cloud-computing/" + file.name;
    axios.put(puturl, file, additionalParams).then((response) => {
      console.log(response.data);
    });
  };

  const match = (e) => {
    e.preventDefault();
    console.log(e.target.value); //exact or quick

    axios
    .post("API-GATEWAY-PATH", {"matchType": e.target.value})
    .then((res) => {
      alert("match Success");
    })
    .catch((err) => alert("match Error"));
  }

  if (!user) {
    return <div>Loading...</div>;
  }

  const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
  axios.get(url, {
    params: {
      email: user.attributes.email
    }
  }).then((response) => {
    console.log(response.data);
  });

  return (
    <Container fluid className="userContainer">
      <Row>
        <Col sm={3} className="avatar">
          <img src={candidate} alt="/"/>
        </Col>
        <Col sm={3}>
        <div className="info">
        <p>Username: {user.attributes.preferred_username}</p>
        <p>Email: {user.attributes.email}</p>
        </div>
        </Col>
        <Col sm={6} className="userBtns">
        <Form action = "" method="POST" onSubmit={uploadResume}>
          <Form.Group controlId="formFile" className="mb-3">
          <Form.Control type="file" onChange={handleChange}/>
          </Form.Group>
          <Button type="submit" variant="primary" size="md" className="uploadBtn">
        Upload Resume
      </Button>
        </Form>
        <Row>
          <Col>
            <Button onClick={match} value="quick" variant="primary" size="md" className="searchBtnsLeft">Quick Match</Button>
            <Button onClick={match} value="exact" variant="primary" size="md" className="searchBtnsRight">Exact Match</Button>
          </Col>
        </Row>
        </Col>
      </Row>
        <Row>
          <img src={"https://resume-of-jrc-cloud-computing.s3.amazonaws.com/${file.name}"} alt="/"></img>
        </Row>
      <Row >
      <h4 className="jobList">Applied Job List</h4>
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
  
export default UserProfile;