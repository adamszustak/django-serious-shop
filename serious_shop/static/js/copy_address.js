$(document).ready(function () {
  const inputsShipping = $(
    'div.shipping input[type=text],div.shipping input[type=email], div.shipping input[type=number]'
  );
  const inputsBilling = $(
    'div.billing input[type=text],div.billing input[type=email], div.billing input[type=number]'
  );
  $('input#addresses').click(function () {
    inputsShipping.each(function () {
      let name = $(this).attr('name').substring(9);
      let billingName = 'div.billing input[name=billing-' + name + ']';
      $(billingName).val($(this).val());
    });
    $('div.billing select.select').val($('div.shipping select.select').val());
  });
});
