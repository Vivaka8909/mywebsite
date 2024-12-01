<script>
const baseRequest = {
  apiVersion: 2,
  apiVersionMinor: 0
};


const validPromoCodes = {
  SOMEPROMOCODE: {
    code: 'SOMEPROMOCODE',
    description: '20% off all products!',
    function: percentageDiscount,
    value: -20
  },
  ANOTHERPROMOCODE: {
    code: 'ANOTHERPROMOCODE',
    description: '$5 dollars off!',
    function: staticDiscount,
    value: -5.00
  }
}

const allowedCardNetworks = ['AMEX', 'DISCOVER', 'JCB', 'MASTERCARD', 'VISA'];

const allowedCardAuthMethods = ['PAN_ONLY', 'CRYPTOGRAM_3DS'];

const tokenizationSpecification = {
  type: 'PAYMENT_GATEWAY',
  parameters: {
    gateway: 'example',
    gatewayMerchantId: 'exampleGatewayMerchantId'
  }
};

const baseCardPaymentMethod = {
  type: 'CARD',
  parameters: {
    allowedAuthMethods: allowedCardAuthMethods,
    allowedCardNetworks: allowedCardNetworks
  }
};

const cardPaymentMethod = Object.assign(
  {},
  baseCardPaymentMethod,
  {
    tokenizationSpecification: tokenizationSpecification
  }
);

let paymentsClient = null;

function getGoogleIsReadyToPayRequest() {
  return Object.assign(
      {},
      baseRequest,
      {
        allowedPaymentMethods: [baseCardPaymentMethod]
      }
  );
}

function getGooglePaymentDataRequest() {
  const paymentDataRequest = Object.assign({}, baseRequest);
  paymentDataRequest.allowedPaymentMethods = [cardPaymentMethod];
  paymentDataRequest.transactionInfo = getGoogleTransactionInfo();
  paymentDataRequest.merchantInfo = {
    merchantName: 'Example Merchant'
  };

  paymentDataRequest.callbackIntents = ['OFFER'];
  paymentDataRequest.shippingAddressRequired = false;
  paymentDataRequest.shippingAddressParameters = getGoogleShippingAddressParameters();

  return paymentDataRequest;
}

function getGooglePaymentsClient() {
  if ( paymentsClient === null ) {
    paymentsClient = new google.payments.api.PaymentsClient({
      environment: 'TEST',
      merchantInfo: {
        merchantName: 'Example Merchant',
        merchantId: '01234567890123456789'
      },
      paymentDataCallbacks: {
        onPaymentDataChanged: onPaymentDataChanged
      }
    });
  }
  return paymentsClient;
}


function percentageDiscount(promoParameters, paymentDataRequestUpdate) {
  
  let originalTransactionInfo = getGoogleTransactionInfo();
  
  let newTransactionInfo = paymentDataRequestUpdate.newTransactionInfo;
  let discount = 0;

    
  paymentDataRequestUpdate.newOfferInfo.offers.push({
    redemptionCode: promoParameters['code'],
    description: promoParameters['description']
  });

  originalTransactionInfo.displayItems.forEach(function(displayItem) {
    discount += parseFloat(displayItem.price) * promoParameters['value'] * 0.01;
  });


  newTransactionInfo.displayItems.push({
      label: promoParameters['code'],
      price: discount.toFixed(2),
      type: 'LINE_ITEM'
  });

  return paymentDataRequestUpdate;
}

function staticDiscount(promoParameters, paymentDataRequestUpdate) {
  let newTransactionInfo = paymentDataRequestUpdate.newTransactionInfo;
  paymentDataRequestUpdate.newOfferInfo.offers.push({
    redemptionCode: promoParameters['code'],
    description: promoParameters['description']
  });

  newTransactionInfo.displayItems.push({
      label: promoParameters['code'],
      price: promoParameters['value'].toFixed(2),
      type: 'LINE_ITEM'
  });

  return paymentDataRequestUpdate;
}


function onPaymentDataChanged(intermediatePaymentData) {
  return new Promise(function(resolve, reject) {

    let redemptionCodes = new Set();
    let shippingOptionData = intermediatePaymentData.shippingOptionData;
    let paymentDataRequestUpdate = {};
    paymentDataRequestUpdate.newTransactionInfo = getGoogleTransactionInfo();

    
    if(typeof intermediatePaymentData.offerData != 'undefined') {
      redemptionCodes = new Set(intermediatePaymentData.offerData.redemptionCodes);
    }


    if (intermediatePaymentData.callbackTrigger === 'OFFER') {
      paymentDataRequestUpdate.newOfferInfo = {};
      paymentDataRequestUpdate.newOfferInfo.offers = [];
      for (redemptionCode of redemptionCodes) {
        if (validPromoCodes[redemptionCode]) {
          paymentDataRequestUpdate = validPromoCodes[redemptionCode].function(
            validPromoCodes[redemptionCode],
            paymentDataRequestUpdate
          );
        } else {
          paymentDataRequestUpdate.error = getGoogleOfferInvalidError(redemptionCode);
        }
      }
    }
    
    paymentDataRequestUpdate.newTransactionInfo = calculateNewTransactionInfo(
      paymentDataRequestUpdate.newTransactionInfo
    )

    resolve(paymentDataRequestUpdate);
  });
}


function calculateNewTransactionInfo(newTransactionInfo) {
  let totalPrice = 0.00;
  newTransactionInfo.displayItems.forEach(
    function(displayItem) {
      totalPrice += parseFloat(displayItem.price);
    }
  );
  newTransactionInfo.totalPrice = totalPrice.toFixed(2);

  return newTransactionInfo;
}


function onGooglePayLoaded() {
  const paymentsClient = getGooglePaymentsClient();
  paymentsClient.isReadyToPay(getGoogleIsReadyToPayRequest())
      .then(function(response) {
        if (response.result) {
          addGooglePayButton();
        }
      })
      .catch(function(err) {
        console.error(err);
      });
}

function addGooglePayButton() {
  const paymentsClient = getGooglePaymentsClient();
  const button =
      paymentsClient.createButton({
        onClick: onGooglePaymentButtonClicked,
        allowedPaymentMethods: [baseCardPaymentMethod]
      });
  document.getElementById('container').appendChild(button);
}

function getGoogleTransactionInfo() {
  return {
        displayItems: [
        {
          label: 'Subtotal',
          type: 'SUBTOTAL',
          price: '11.00',
          status: 'FINAL'
        },
        {
          label: 'Tax',
          type: 'TAX',
          price: '1.00'
        }
    ],
    currencyCode: 'USD',
    totalPriceStatus: 'FINAL',
    totalPrice: '12.00',
    totalPriceLabel: 'Total'
  };
}

function getGoogleShippingAddressParameters() {
        return  {
        allowedCountryCodes: ['US', 'UK', 'FR', 'CA', 'MX', 'GA'],
    phoneNumberRequired: false
  };
}

function getGoogleOfferInvalidError(redemptionCode) {
        return {
    reason: 'OFFER_INVALID',
    message: redemptionCode + ' is not a valid promo code.',
    intent: 'OFFER'
        };
}

function prefetchGooglePaymentData() {
  const paymentDataRequest = getGooglePaymentDataRequest();
  paymentDataRequest.transactionInfo = {
    totalPriceStatus: 'NOT_CURRENTLY_KNOWN',
    currencyCode: 'USD'
  };
  const paymentsClient = getGooglePaymentsClient();
  paymentsClient.prefetchPaymentData(paymentDataRequest);
}
function onGooglePaymentButtonClicked() {
  const paymentDataRequest = getGooglePaymentDataRequest();
  paymentDataRequest.transactionInfo = getGoogleTransactionInfo();

  const paymentsClient = getGooglePaymentsClient();
  paymentsClient.loadPaymentData(paymentDataRequest)
      .then(function(paymentData) {
        processPayment(paymentData);
      })
      .catch(function(err) {
        console.error(err);
      });
}


function processPayment(paymentData) {
  
    console.log(paymentData);
  
  paymentToken = paymentData.paymentMethodData.tokenizationData.token;
}</script>
<script async
  src="https://pay.google.com/gp/p/js/pay.js"
  onload="onGooglePayLoaded()"></script>
</div>
    </div>