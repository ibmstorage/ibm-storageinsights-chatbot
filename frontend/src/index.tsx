import React from "react";
import ReactDOM from "react-dom";
import "./index.scss";
import { HashRouter } from "react-router-dom";
import App from "src/App";

const Index = () => {
  return (
    <React.StrictMode>
      <HashRouter>
        <App />
      </HashRouter>
    </React.StrictMode>
  );
};

ReactDOM.render(<Index />, document.getElementById("root"));
