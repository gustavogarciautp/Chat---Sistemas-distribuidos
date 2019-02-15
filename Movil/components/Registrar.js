import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  Image,
  Button,
  TextInput,
  Alert,
  Picker,
} from 'react-native';
import { createStackNavigator, createAppContainer } from 'react-navigation';
import io from 'socket.io-client';

//const net= require('net');

export default class Registrar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Nombre: '',
      Apellido: '',
      Login: '',
      Password: '',
      Edad: '',
      Genero: 'Genero'
    };
  }

 validacion() {
    this.socket.emit('Registrarse',JSON.stringify(this.state), (answer)=>{
        answer=JSON.parse(answer)
        if (answer){
          Alert.alert('Error',answer)
          this.setState({Login:'',Password:''})
          }
        else{
          this.props.navigation.navigate('Sesion',{socket:this.socket})
        }
    })
  }

  render() {
    const { navigation } = this.props;
    this.socket = navigation.getParam('socket');
    return (
      <View style={{ flex: 1, flexDirection: 'row', padding: 0 }}>
        <View
          style={{
            flex: 0.4,
            flexDirection: 'column',
            justifyContent: 'center',
            backgroundColor: '#B8CDE3',
          }}>
          <View style={{ height: 100 }}>
            <Image
              source={require('./../assets/logo.png')}
              style={{
                height: 80,
                width: 80,
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            />
          </View>
        </View>
        <View
          style={{
            backgroundColor: '#6D7B8F',
            flex: 0.6,
            flexDirection: 'column',
            justifyContent: 'center',
          }}>
          <View style={{ paddingLeft: 20, paddingRight: 20 }}>
            <TextInput
              style={{
                height: 40,
                backgroundColor: 'white',
                marginBottom: 35,
                textAlign: 'center',
              }}
              placeholder="Nombre"
              onChangeText={Nombre => this.setState({ Nombre })}
              value={this.state.Nombre}
            />

            <TextInput
              style={{
                height: 40,
                backgroundColor: 'white',
                marginBottom: 35,
                textAlign: 'center',
              }}
              placeholder="Apellidos"
              onChangeText={Apellido => this.setState({ Apellido })}
            />

            <TextInput
              style={{
                height: 40,
                backgroundColor: 'white',
                marginBottom: 35,
                textAlign: 'center',
              }}
              placeholder="Usuario"
              onChangeText={Login => this.setState({ Login })}
            />
            <TextInput
              style={{
                height: 40,
                backgroundColor: 'white',
                marginBottom: 35,
                textAlign: 'center',
              }}
              placeholder="Contraseña"
              secureTextEntry={true}
              onChangeText={Password => {
                this.setState({ Password });
              }}
            />
            <TextInput
              style={{
                height: 40,
                backgroundColor: 'white',
                marginBottom: 35,
                textAlign: 'center',
              }}
              placeholder="Edad"
              onChangeText={Edad => this.setState({ Edad })}
            />

            <Picker
              mode='dialog'
              selectedValue={this.state.Genero}
              onValueChange={(itemValue, itemIndex) =>
                this.setState({ Genero: itemValue })
              }
              style={{
                height: 40,
                backgroundColor: 'white',
                alignContent: 'center',
                marginBottom: 35,
              }}
              itemStyle={{ textAlign: 'center' }}>
              <Picker.Item label="Género" value="" />
              <Picker.Item label="Masculino" value="Masculino" />
              <Picker.Item label="Femenino" value="Femenino" />
              <Picker.Item label="Otros" value="Otros" />
            </Picker>

            <Button title="Aceptar" onPress={this.validacion.bind(this)} />
          </View>
        </View>
      </View>
    );
  }
}
