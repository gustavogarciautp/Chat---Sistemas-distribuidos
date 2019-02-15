import React from "react";
import { View, Text, Button, Alert } from "react-native";
import { createStackNavigator, createAppContainer } from "react-navigation";
import Inicio_sesion from "./components/Inicio_sesion"
import Registrar from "./components/Registrar"
import Salaprincipal from "./components/salap"
const io = require ( 'socket.io-client' );

class HomeScreen extends React.Component {

  componentDidMount(){

    this.socket = io('http://192.168.0.13:8000');
  }

  
  render() {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <Button title="Inicio Sesion" onPress={() => this.props.navigation.navigate('Sesion', {
              socket: this.socket
            })} />
        <Button title="Registrar" onPress={() => this.props.navigation.navigate('Registro',{
              socket: this.socket
            })} />
      </View>
    );
  }
}

const AppNavigator = createStackNavigator(
  {
    Home: HomeScreen,
    Sesion: Inicio_sesion,
    Registro: Registrar,
    Sala: Salaprincipal
  },
  {
    initialRouteName: "Home"
  }
);

export default createAppContainer(AppNavigator);