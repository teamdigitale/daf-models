import React from 'react';
import PredictionsTable from './PredictionsTable';

export default class ClassifierForm extends React.Component {
  constructor() {
    super();
    this.state = {
      sentence: 'L.R. 3/94 Art. 37: autorizzazione interventi di controllo sulle specie Cornacchia grigia (Corvus corone Cornix) e Gazza (Pica pica) _NUI AR/18/76 e AR/18/77.',
      response: '',
      isLoaded: false,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    console.log(process.env.NODE_ENV);

    let url = "/predict";

    if (process.env.NODE_ENV === "development"){
      url = "http://localhost:5000/predict"
    }

    fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body : JSON.stringify({
        sentence: this.state.sentence
      })
    }).then((response) => {
        return response.json();
    }).then(
      (data) => {
        this.setState({
          response: data,
          isLoaded: true
        });
        console.log(data);
      },
      (error) => {
        this.setState({
          response: error,
          isLoaded: true
        });
        console.log(JSON.stringify(error))
    });
  }

  handleChange(event) {
    this.setState({sentence: event.target.value});
  }

  render() {
    const { isLoaded, response} = this.state;
    if (!isLoaded){
      return (
        <form onSubmit={this.handleSubmit}>
          <div className="input-group">
            <div className="input-group-prepend">
              <span className="input-group-text">Oggetto</span>
            </div>
            <textarea className="form-control" id="sentence" rows="3" value={this.state.sentence} onChange={this.handleChange}/>
          </div>
          <button className="btn btn-primary" >Classify</button>
        </form>
      )
    } else {
      return (
        <div className="container-fluid">
          <div className="row">
            <div className="col">
              <form onSubmit={this.handleSubmit}>
                <div className="input-group">
                  <div className="input-group-prepend">
                    <span className="input-group-text">Oggetto</span>
                  </div>
                  <textarea className="form-control" id="sentence" rows="3" value={this.state.sentence} onChange={this.handleChange}/>
                </div>
                <button className="btn btn-primary">Classify</button>
              </form>
            </div>
          </div>
          <div className="row">
            <div className="col"><p></p></div>
          </div>
          <div className="row">
            <h4>Predictions</h4>
          </div>
          <div className="row">
            <PredictionsTable  predictions={response.prediction_probabilities}/>
          </div>
      </div>
      );
    }
  }
}
