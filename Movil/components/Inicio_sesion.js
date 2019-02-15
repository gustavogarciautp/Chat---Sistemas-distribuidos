import React from 'react';
import { StyleSheet, Text, View, Image, Button, TextInput ,Alert} from 'react-native';
import { createStackNavigator, createAppContainer } from 'react-navigation';

class Inicio_sesion extends React.Component {
  constructor(props) {
    super(props);
     this.state = { 
       Login: '',
       Password: ''
       };
  }

  startsession(){
    this.socket.emit('startsession',JSON.stringify(this.state),(answer)=>{
        answer=JSON.parse(answer)
        if (answer){
          Alert.alert('Error',answer)
          this.setState({Login:'',Password:''})
          }
        else{
          this.props.navigation.navigate('Sala',{socket:this.socket})
        }
    })
}

    render() {
      const { navigation } = this.props;
      this.socket = navigation.getParam('socket');
      return (
        <View style={{flex: 1, flexDirection: 'row', padding:0}}>
          <View style={{flex:0.4, flexDirection:'column', justifyContent:'center', backgroundColor: '#B8CDE3'}}>
            <View style={{height:100}}>
              <Image source={require('./../assets/logo.png')}
            style={{height:80, width:80, marginLeft: 'auto',marginRight: 'auto'}}/>  

            </View>
          </View>
          <View style={{backgroundColor: '#6D7B8F',flex:0.6, flexDirection: 'column', justifyContent: 'center'}}>
            <View style={{paddingLeft:20, paddingRight:20}}>
              <TextInput
              style={{height: 40, backgroundColor: 'white', marginBottom:50, textAlign:"center"}}
              placeholder="Usuario"
              onChangeText={Login => this.setState({ Login })}
              value={this.state.Login}
              />

              <TextInput style={{height: 40, backgroundColor: 'white', marginBottom:50, textAlign:"center"}}
                placeholder="Contraseña"
                secureTextEntry={true}
                onChangeText={Password => this.setState({Password})}
                value={this.state.Password}
              />

              <Button
                title="Aceptar" onPress={this.startsession.bind(this)}
              />
            </View>
          </View>
        </View>
      );
    }
  }

export default Inicio_sesion