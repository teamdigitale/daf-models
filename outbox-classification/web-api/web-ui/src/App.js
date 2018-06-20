import React, {Component} from 'react';
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
                        <h4 className="display-3 mb-0">Acts Classifier for Regione Toscana</h4>
                        <h5 className="m-0 ml-1">This pages shows a demo of an automatic classifier of the
                            administrative acts published by Regione Toscana</h5>
                    </div>
                </header>

                <nav className="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
                    <div className="container">
                        <button className="navbar-toggler" type="button" data-toggle="collapse"
                                data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup"
                                aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                            <div className="navbar-nav">
                                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white"
                                   href="#definition">Introduction</a>
                                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white"
                                   href="#demo">Demo</a>
                                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white"
                                   href="#approach">Approach</a>
                                <a className="nav-item nav-link text-white pl-3 pr-3 mr-3 border border-white"
                                   href="#api">Api Endpoint</a>
                            </div>
                        </div>
                    </div>
                </nav>

                <div className="container">
                    <section>
                        <h2 id="definition" className="pt-5 pb-3">Introduction</h2>
                        <div className="">
                            Artificial Intelligence can be used by Public Administration to automate several labour
                            intensive tasks. The goal of this application is to show
                            how in the <a href="https://teamdigitale.governo.it/en/">Digital Transformation Team</a> we
                            apply <a href="https://en.wikipedia.org/wiki/Machine_learning">Machine Learning</a> to
                            classify the <a href="">Regional Acts</a> published by <a>Regione Toscana</a>.
                            We have exposed a classifier via <a
                            href="https://en.wikipedia.org/wiki/Representational_state_transfer">rest api</a> that can
                            be used to automatically categorize the published documents.
                        </div>
                    </section>

                    <section>
                        <h2 id="demo" className="pt-5 pb-3">Demo</h2>
                        <p>In order to test the service open the page <a
                            href="http://www.regione.toscana.it/bancadati/atti/"> Atti Dirigenti</a> and paste the
                            subject of the acts in the textarea below.</p>
                        <ClassifierForm/>
                    </section>

                    <section>
                        <h2 id="approach" className="pt-5 pb-3">Approach</h2>
                        <div className="">
                            <p>In order to build the classifier we crawled 184.381 documents, which were split into
                                training, validation and test set. The model is built using a neural network implemented
                                in <a href="https://keras.io/">Keras</a>. The steps done to build the model were:</p>
                            <ol>
                                <li><a
                                    href="https://github.com/teamdigitale/daf-models/blob/master/outbox-classification/notebook/preprocessing/data_preprocessing.ipynb">data
                                    wrangling and exploration</a></li>
                                <li>to build a <a
                                    href="https://github.com/teamdigitale/daf-models/blob/master/outbox-classification/notebook/1_baseline.ipynb">basic
                                    classifier</a> that uses Neural Networks
                                </li>
                                <li><a
                                    href="https://github.com/teamdigitale/daf-models/blob/master/outbox-classification/notebook/2_regularization.ipynb">how
                                    to use regularization</a> to improve the model accuracy while addressing overfitting
                                </li>
                                <li>the effect of <a
                                    href="https://github.com/teamdigitale/daf-models/blob/master/outbox-classification/notebook/4_embeddings.ipynb">distributed
                                    representations of words </a> to improve the models
                                </li>
                                <li>analyze the effect of <a
                                    href="https://github.com/teamdigitale/daf-models/blob/master/outbox-classification/notebook/5_recurrent_neural_network.ipynb">using
                                    sequence of text </a></li>
                                <li>how to deploy the model <a
                                    href="https://github.com/teamdigitale/daf-models/tree/master/outbox-classification/web-api"> as
                                    a web service</a></li>
                            </ol>
                            <p>Below there is the final model with parameters tuned. Further details about what was done
                                can be found <a
                                    href="https://github.com/teamdigitale/daf-models/tree/master/outbox-classification">here</a>.
                            </p>
                        </div>

                        <div className="">
                            <p>The classifier was trained to detect the following classes.</p>
                            <ClassTable></ClassTable>
                            When the classifier is not sure about the class its prediction probability will drop to
                            values below 0.99.
                        </div>
                    </section>

                    <section>
                        <h2 id="api" className="pt-5 pb-3">API</h2>
                        <div className="card">
                            <div className="card-body">
                                <p>To consume the service via API: <br/>
                                    <code>curl -XPOST -H "Content-Type: application/json"
                                        -d &apos;&#123;"sentence":"sentence to be
                                        classified"&#125;&apos; https://ml-api.daf.teamdigitale.it/predict</code>
                                </p>
                            </div>
                        </div>
                    </section>
                    <section>
                        <div className="row">
                            <br/>
                        </div>
                    </section>
                    <section>
                        <footer className="blockquote-footer jumbotron-fluid ">
                            <h5>
                                <a href="https://teamdigitale.governo.it">Team Digitale</a> © 2018 Team Digitale.
                                <span className="float-right">Powered by<a href="https://teamdigitale.governo.it">Team Digitale</a></span>
                            </h5>
                        </footer>
                    </section>
                </div>
            </div>
        );
    }
}

export default App;
