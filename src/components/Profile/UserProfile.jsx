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
  const [resume, setResume] = useState(null);
  const [username, setUsername] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        const user = await Auth.currentAuthenticatedUser();
        setUser(user);
        const response = axios.head("https://resume-of-jrc-cloud-computing.s3.amazonaws.com/" + user.attributes.email);
      setResume("https://resume-of-jrc-cloud-computing.s3.amazonaws.com/" + user.attributes.email);
      console.log("success");
      const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
      axios.get(url, {
        params: {
          email: user.attributes.email
        }
      }).then((response) => {
        console.log(response.data);
        setUsername(response.data.username);
      });
      } catch (error) {
        console.log(error);
      }
    }
    fetchUser();
  }, []);

  /*
  async function fetchResume() {
    try {
      const response = await axios.head("https://resume-of-jrc-cloud-computing.s3.amazonaws.com/" + user.attributes.email);
      setResume("https://resume-of-jrc-cloud-computing.s3.amazonaws.com/" + user.attributes.email);
      console.log("success");
    } catch(error) {
      console.log(error);
    }
  }
  fetchResume();*/

  //console.log(user)

  const [file, setFile] = useState()
  function handleChange(event) {
    setFile(event.target.files[0])
  }
  const uploadResume = (event) => {
    event.preventDefault(); // prevent the form from submitting
    console.log(file.type.split("/").pop());
    
    var additionalParams = {
			headers: {
        "Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Headers": "*",
				"Access-Control-Allow-Methods": "PUT",
				"Content-Type": file.type,
			},
		};

    const puturl = "https://794k191dy4.execute-api.us-east-1.amazonaws.com/v1/upload/resume-of-jrc-cloud-computing/" + user.attributes.email;
    axios.put(puturl, file, additionalParams).then((response) => {
      console.log(response.data);
      setResume("https://resume-of-jrc-cloud-computing.s3.amazonaws.com/" + user.attributes.email)
      alert("You have uploaded your resume successfully! \n\n Feel free to try our matching services.");
      window.location.reload();
      //window.location.reload();
    }).catch((error) => {
      console.log(error);
      alert("Oops, something goes wrong. Please try to upload again.");
    });
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  /*
  const url = "https://xs4bmp3o2l.execute-api.us-east-1.amazonaws.com/jugotest/profile";
  axios.get(url, {
    params: {
      email: user.attributes.email
    }
  }).then((response) => {
    console.log(response.data);
    setUsername(response.data.username);
  });*/
  
  return (
    <Container fluid className="userContainer">
      <Row>
        <Col sm={3} className="avatar">
          <img src={candidate} alt="/"/>
        </Col>
        <Col sm={3}>
        <div className="info">
        <p>Username: {username}</p>
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
        {
        resume ?
          <Col>
            <Button href="/quick-match" variant="primary" size="md" className="searchBtnsLeft">Quick Match</Button>
            <Button href="/exact-match" value="exact" variant="primary" size="md" className="searchBtnsRight">Exact Match</Button>
          </Col> : null}
        </Row>
        </Col>
      </Row>
      {
        resume ?
        <Row>
        <Col className="resumePic">
          <img src={resume} alt="Please Upload Your Resume" className="resume"></img>
          </Col>
        </Row> : null

      }
     
      {/** 
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
      </Row>*/}

    </Container>
  );
};
  
export default UserProfile;