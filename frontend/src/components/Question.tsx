import React, { Component } from 'react';
import '../stylesheets/Question.css';

type IProps = {
    question: string,
    answer: string,
    category: string,
    difficulty: number,
    questionAction: Function
}
type IState = {
    visibleAnswer: boolean
}

class Question extends Component<IProps, IState> {
    state: IState = {
        visibleAnswer: false
    }

    flipVisibility() {
        this.setState({ visibleAnswer: !this.state.visibleAnswer });
    }

    render() {
        const { question, answer, category, difficulty } = this.props;
        return (
            <div className="Question-holder">
                <div className="Question">{question}</div>
                <div className="Question-status">
                    <img className="category" src={`${category?.toLowerCase()}.svg`} />
                    <div className="difficulty">Difficulty: {difficulty}</div>
                    <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')} />

                </div>
                <div className="show-answer button"
                    onClick={() => this.flipVisibility()}>
                    {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
                </div>
                <div className="answer-holder">
                    <span style={{ "visibility": this.state.visibleAnswer ? 'visible' : 'hidden' }}>Answer: {answer}</span>
                </div>
            </div>
        );
    }
}

export default Question;
