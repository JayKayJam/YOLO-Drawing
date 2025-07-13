import './Colors.css';
import { useState } from 'react';

// TODO: Make border colors variable i.e. change colors when clicked
function Colors() {
  return (
    <div style={{ textAlign: 'left' }}>
      <h3>Color List</h3>
      <hr style={{ width: 75, marginLeft: 0 }} />
      <button id="eraseButton"> Erase </button>
      <div></div>
      <button id="redButton"> Red </button>
      <div></div>
      <button id="greenButton"> Green </button>
    </div>
  );
}

export default Colors;
