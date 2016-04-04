/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 */
'use strict';
import React, {
  AppRegistry,
  Component,
  StyleSheet,
  TextInput,
  View
} from 'react-native';

var UIParams=require("./ui_params");
var utils=require("./utils");

class FieldDecimal extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        var val=this.props.data[this.props.name];
        this.setState({value:val});
    }

    load_data() {
    }

    render() {
        var f=UIParams.get_field(this.props.model,this.props.name);
        var val_str=utils.field_val_to_str(this.state.value,f);
        return <TextInput value={val_str} onChangeText={this.onchange.bind(this)} style={{height:40}}/>
    }

    onchange(val) {
        this.setState({value:val});
        this.props.data[this.props.name]=val;
    }
}

module.exports=FieldDecimal;
