var SPMaskBehavior = function (val) {
  return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};

var options = {
  onKeyPress: function (cpf, ev, el, op) {
      var masks = ['000.000.000-000', '00.000.000/0000-00'];
      $('.mask_cpfcnpj').mask((cpf.length > 14) ? masks[1] : masks[0], op);
  }
}

$(function(){
  $('.mask_telefone').mask(SPMaskBehavior, spOptions);
  $('.mask_cep').mask('00000-000');  
  $('.mask_cpfcnpj').length > 11 ? $('.mask_cpfcnpj').mask('00.000.000/0000-00', options) : $('.mask_cpfcnpj').mask('000.000.000-00#', options);
  $('.mask_money').mask("###0,00", {reverse: true});
  /* $(".mask_money").inputmask('Regex', {regex: "^[0-9]{1,6}(\\,\\d{1,2})?$"}); */
});


