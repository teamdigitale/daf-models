import React, { Component } from 'react';
import './App.css';
import ClassifierForm from './ClassifierForm';
import 'bootstrap/dist/css/bootstrap.min.css';
import ClassTable from './ClassTable';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="bg-primary">
          <div className="container text-white pt-6 pb-6">
            <h1 className="display-1 display-1 mb-0">Text Classification App</h1>
            <p className="m-0 ml-1">This pages shows a demo of an automatic classifier of the administrative acts published by Regione Toscana</p>
          </div>
        </header>

        <nav className="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
          <div className="container">
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
              <div className="navbar-nav">
                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white" href="#definition">Introduction</a>
                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white" href="#demo">Demo</a>
                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white" href="#approach">Approach</a>
                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white" href="#api">Api Endpoint</a>
              </div>
            </div>
          </div>
        </nav>

        <div className="container">
          <section >
            <h2 id="definition" className="pt-5 pb-3">Introduction</h2>
            <div className="">
                Artificial Intelligence can be used by Public Administration to automate several labour intensive tasks. The goal of this application is to show
                how in the  <a href="https://teamdigitale.governo.it/en/">Digital Transformation Team</a> we apply <a href="https://en.wikipedia.org/wiki/Machine_learning">Machine Learning</a> to
                classify the <a href="">Regional Acts</a> published by <a>Regione Toscana</a>.
                 We have exposed a classifier via <a href="https://en.wikipedia.org/wiki/Representational_state_transfer">rest api</a> that can be used to automatically categorize the published documents.
            </div>
          </section>

          <section >
            <h2 id="demo" className="pt-5 pb-3">Demo</h2>
            <p>In order to test the service open the page <a href="http://www.regione.toscana.it/bancadati/atti/"> Atti Dirigenti</a> and paste the subject of the acts in the textarea below.</p>
            <ClassifierForm />
          </section>

          <section >
            <h2 id="approach" className="pt-5 pb-3">Approach</h2>
            <div className="">
                In order to build the classifier we crawled 152455 documents, which where split into training, validation and test set. The model is built using a neural network inmplemented in
                <a href="https://keras.io/">Keras</a>. The steps done to built the model were:
                  <ol>
                    <li>data wrangling and exploration</li>
                    <li>to build a <a href="">basic classifier</a> that uses Neural Networks</li>
                    <li><a href="">how to use regularization</a> to improve the model accuracy while addressing over-fitting </li>
                    <li>the effect of <a href="">distributed representations of words </a> to improve the models</li>
                    <li>analyze the effect of using sequence of text <a href=""></a></li>
                    <li><a href="">Hyper-Parameters Optimization</a></li>
                    <li>how to deploy the model <a href="as a web service"></a></li>
                  </ol>
                What you can use below if the final model with parameters tuned. More detaails about what was done can be found <a href="">here</a>.
            </div>

            <div className="">
              The classifier was trained to detect the following classes.
              <ClassTable></ClassTable>
              You can see that when the classifier is not sure about the class its prediction probability will drop to values below 0.8.
            </div>
          </section>

          <section >
            <h2 id="api" className="pt-5 pb-3">API</h2>
              <div className="card">
                <div className="card-body">
                  To consume the service via API: <code>curl -XPOST -H "Content-Type: application/json" -d &apos;&#123;"sentence":"sentence to be classified"&#125;&apos; </code>
                </div>
              </div>
          </section>
        </div>

      </div>
    );
  }
}

export default App;
