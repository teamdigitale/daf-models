import React from 'react';
import { Table } from 'reactstrap';

export default class ClassTable extends React.Component {
  constructor(){
    super();
    this.state = {
         "01943":0,
         "DIREZIONE GENERALE SVILUPPO ECONOMICO                 ":1,
         "01946":2,
         "01025":3,
         "D.G. PRESIDENZA                                       ":4,
         "01934":5,
         "DIREZIONE GENERALE DIRITTO ALLA SALUTE E POLITICHE DI ":6,
         "DIREZIONE GENERALE POLITICHE TERRITORIALI E AMBIENTALI":7,
         "01937":8,
         "D.G.  AVVOCATURA                                      ":9,
         "01928":10,
         "POLITICHE AMBIENTALI, ENERGIA E CAMBIAMENTI CLIMATICI":11,
         "DIREZIONE ORGANIZZAZIONE E SISTEMI INFORMATIVI":12,
         "DIREZIONE GENERALE BILANCIO E FINANZE                 ":13,
         "DIREZIONE DIFESA DEL SUOLO E PROTEZIONE CIVILE":14,
         "DIREZIONE GENERALE POLITICHE FORMATIVE, BENI E ATTIVIT":15,
         "D.G. COMPETITIVITA' DEL SISTEMA REGIONALE E SVILUPPO D":16,
         "DIREZIONE DIRITTI DI CITTADINANZA E COESIONE SOCIALE":17,
         "DIREZIONE ISTRUZIONE E FORMAZIONE":18,
         "DIREZIONE AGRICOLTURA E SVILUPPO RURALE":19
      }
  }
  render(){
    return (
      <Table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Office Name</th>
          </tr>
        </thead>
        <tbody>
          {
            Object.keys(this.state).map((key, index) => (
            <tr key={index}>
              <th scope="row">{index}</th>
              <td>{key}</td>
            </tr>
          ))
        }
        </tbody>
      </Table>
    );
  }
}
