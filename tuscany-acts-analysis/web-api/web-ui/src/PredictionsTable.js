import React from 'react';
import { Table } from 'reactstrap';

export default class PredictionsTable extends React.Component {

  render(){

    const array = Object.keys(this.props.predictions).map(key => {
      return [key, this.props.predictions[key]];
    });

    array.sort((a,b) => {
      return b[1] - a[1];
    });

    return (
      <Table>
        <thead>
          <tr>
            <th>Office Name</th>
            <th>Probability</th>
          </tr>
        </thead>
        <tbody>
          {
            array.map((a) => {
              return <tr>
                <td>{a[0]}</td>
                <td>{a[1]}</td>
              </tr>
            })
        }
        </tbody>
      </Table>
    );
  }
}
