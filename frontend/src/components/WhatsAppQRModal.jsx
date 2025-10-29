import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { useToast } from '../hooks/use-toast';
import { X, CheckCircle, Loader2, RefreshCw, Smartphone } from 'lucide-react';
import { integrationsAPI } from '../utils/api';

const WhatsAppQRModal = ({ isOpen, onClose, chatbotId, onSuccess }) => {
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [qrCode, setQrCode] = useState(null);
  const [checking, setChecking] = useState(false);
  const [connected, setConnected] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState(null);
  const [sessionToken, setSessionToken] = useState(null);

  useEffect(() => {
    if (isOpen) {
      generateQRCode();
    } else {
      // Reset state when modal closes
      setQrCode(null);
      setConnected(false);
      setPhoneNumber(null);
      setSessionToken(null);
    }
  }, [isOpen]);

  useEffect(() => {
    let interval;
    if (qrCode && !connected) {
      // Check connection status every 2 seconds
      interval = setInterval(() => {
        checkConnectionStatus();
      }, 2000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [qrCode, connected]);

  const generateQRCode = async () => {
    try {
      setLoading(true);
      const response = await integrationsAPI.generateWhatsAppQR(chatbotId);
      setQrCode(response.data.qr_code);
      setSessionToken(response.data.session_token);
    } catch (error) {
      console.error('Error generating QR code:', error);
      toast({
        title: 'Error',
        description: 'Failed to generate QR code',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const checkConnectionStatus = async () => {
    if (checking) return;
    
    try {
      setChecking(true);
      const response = await integrationsAPI.checkWhatsAppStatus(chatbotId);
      
      if (response.data.connected) {
        setConnected(true);
        setPhoneNumber(response.data.phone_number);
        toast({
          title: 'Connected!',
          description: 'WhatsApp connected successfully'
        });
        if (onSuccess) onSuccess();
      }
    } catch (error) {
      console.error('Error checking status:', error);
    } finally {
      setChecking(false);
    }
  };

  const simulateConnection = async () => {
    // This is for demo purposes - simulates scanning the QR code
    try {
      await integrationsAPI.simulateWhatsAppConnect(chatbotId);
      await checkConnectionStatus();
    } catch (error) {
      console.error('Error simulating connection:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full relative animate-fade-in-up">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-green-700 p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center">
                <svg className="w-7 h-7 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Connect WhatsApp</h2>
                <p className="text-green-100 text-sm">Scan QR code to link device</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-green-700 p-2 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="p-6">
          {!connected ? (
            <div className="space-y-4">
              {/* QR Code */}
              <div className="bg-gray-50 rounded-xl p-6 flex flex-col items-center">
                {loading ? (
                  <div className="w-64 h-64 flex items-center justify-center">
                    <Loader2 className="w-12 h-12 animate-spin text-green-600" />
                  </div>
                ) : qrCode ? (
                  <>
                    <img 
                      src={qrCode} 
                      alt="WhatsApp QR Code" 
                      className="w-64 h-64 border-4 border-green-600 rounded-xl shadow-lg"
                    />
                    {checking && (
                      <div className="mt-4 flex items-center gap-2 text-green-600">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span className="text-sm">Checking connection...</span>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="w-64 h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-xl">
                    <p className="text-gray-500">QR Code will appear here</p>
                  </div>
                )}
              </div>

              {/* Instructions */}
              <div className="bg-gradient-to-r from-blue-50 to-green-50 border-2 border-green-200 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <Smartphone className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div className="space-y-2">
                    <h3 className="font-semibold text-gray-900">How to connect:</h3>
                    <ol className="text-sm text-gray-700 space-y-1 list-decimal list-inside">
                      <li>Open WhatsApp on your phone</li>
                      <li>Tap Menu or Settings → Linked Devices</li>
                      <li>Tap "Link a Device"</li>
                      <li>Point your phone at this screen to scan the QR code</li>
                    </ol>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button
                  onClick={generateQRCode}
                  disabled={loading}
                  className="flex-1 bg-gray-600 hover:bg-gray-700"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh QR Code
                </Button>
                
                {/* Demo Button - Remove in production */}
                <Button
                  onClick={simulateConnection}
                  disabled={loading || !qrCode}
                  className="flex-1 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800"
                >
                  Demo: Simulate Scan
                </Button>
              </div>
            </div>
          ) : (
            /* Connected State */
            <div className="text-center py-8">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-12 h-12 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Connected!</h3>
              <p className="text-gray-600 mb-1">WhatsApp successfully linked</p>
              {phoneNumber && (
                <p className="text-sm text-gray-500 font-mono">{phoneNumber}</p>
              )}
              <Button
                onClick={onClose}
                className="mt-6 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800"
              >
                Done
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WhatsAppQRModal;
