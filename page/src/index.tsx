import React from 'react';
import ReactDOM from 'react-dom';

import './pure.css';
import './App.scss';

interface FormProps {
  APIServer: string;
}

const initialState = {
  nickname: "",
  email: "",
  website: "",
  body: "",
}

class Form extends React.Component<FormProps> {

  state = initialState

  onBodyChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    this.setState({ [event.target.name]: event.target.value })
  }

  onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({ [event.target.name]: event.target.value })
  }

  reset = (event: React.FormEvent) => {
    this.setState(initialState)
    event.preventDefault()
  }

  submit = (event: React.FormEvent) => {
    console.log(this.state)
    event.preventDefault()
  }

  render() {
    return (
      <form className="form" onSubmit={this.submit} onReset={this.reset}>
        <div className="pure-g other-data">
          <input className="pure-u-1 pure-u-sm-1-3" type="text" name="nickname" value={this.state.nickname} placeholder="昵称" onChange={this.onChange} />
          <input className="pure-u-1 pure-u-sm-1-3" type="email" name="email" value={this.state.email} placeholder="邮箱" onChange={this.onChange} />
          <input className="pure-u-1 pure-u-sm-1-3" type="url" name="website" value={this.state.website} placeholder="网址" onChange={this.onChange} />
        </div>
        <div className="pure-g body">
          <textarea rows={8} className="pure-u-1" name="body" value={this.state.body} placeholder="想说些什么呢?" onChange={this.onBodyChange}></textarea>
        </div>
        <div className="footer">
          <div style={{ float: "left" }}>
            <a href="https://github.com/abersheeran/Trotter">Trotter</a>
          </div>
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <button type="reset">清空</button>
            <button type="submit">提交</button>
          </div>
        </div>
      </form>
    )
  }
}


const App: React.FC = () => {
  return (
    <div className="trotter">
      <Form APIServer="https://trotter-comment.aber.sh" />
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('Trotter'));
