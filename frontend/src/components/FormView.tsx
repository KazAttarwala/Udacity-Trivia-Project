import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

export type FixMeLater = any;

type IState = {
    question: string,
    answer: string,
    difficulty: number,
    category: number,
    categories: FixMeLater
}

type IProps = {

}

class FormView extends Component<IProps, IState> {
    state: IState = {
        question: "",
        answer: "",
        difficulty: 1,
        category: 1,
        categories: {}
    };

    componentDidMount() {
        $.ajax({
            url: `/categories`, 
            type: "GET",
            success: (result) => {
                this.setState({ categories: result.categories })
                return;
            },
            error: () => {
                alert('Unable to load categories. Please try your request again')
                return;
            }
        })
    }

    submitQuestion = (event: FixMeLater) => {
        event.preventDefault();
        $.ajax({
            url: '/questions', 
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                question: this.state.question,
                answer: this.state.answer,
                difficulty: this.state.difficulty,
                category: this.state.category
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: () => {
                const form = document.getElementById("add-question-form") as HTMLFormElement;
                form.reset();
                return;
            },
            error: () => {
                alert('Unable to add question. Please try your request again')
                return;
            }
        })
    }

    handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>): void => {
        this.setState({ [event.target.name]: event.target.value } as unknown as Pick<IState, keyof IState>)
    }

    render() {
        return (
            <div id="add-form">
                <h2>Add a New Trivia Question</h2>
                <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
                    <label>
                        Question
                        <input type="text" name="question" onChange={this.handleChange} />
                    </label>
                    <label>
                        Answer
                        <input type="text" name="answer" onChange={this.handleChange} />
                    </label>
                    <label>
                        Difficulty
                        <select name="difficulty" onChange={this.handleChange}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </label>
                    <label>
                        Category
                        <select name="category" onChange={this.handleChange}>
                            {Object.keys(this.state.categories).map(id => {
                                return (
                                    <option key={id} value={id}>{this.state.categories[id]}</option>
                                )
                            })}
                        </select>
                    </label>
                    <input type="submit" className="button" value="Submit" />
                </form>
            </div>
        );
    }
}

export default FormView;
