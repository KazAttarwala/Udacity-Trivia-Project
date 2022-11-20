import React, { Component, FormEvent } from 'react'
import { FixMeLater } from './FormView'

type IProps = {
    submitSearch: Function
}

class Search extends Component<IProps> {
    state = {
        query: '',
    }

    getInfo = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        this.props.submitSearch(this.state.query)
    }

    handleInputChange = () => {
        this.setState({
            query: this.search!.value
        })
    }
    search: FixMeLater
    render() {
        return (
            <form onSubmit={this.getInfo}>
                <input
                    placeholder="Search questions..."
                    ref={input => this.search = input}
                    onChange={this.handleInputChange}
                />
                <input type="submit" value="Submit" className="button" />
            </form>
        )
    }
}

export default Search
