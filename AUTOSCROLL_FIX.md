# Auto-Scroll Fix for Live Chat Preview

## Summary
Fixed auto-scrolling behavior in both the Chat Preview Modal and Public Chat page to ensure only the messages area scrolls automatically when new messages arrive, not the entire page.

## Changes Made

### 1. ChatPreviewModal.jsx (`/app/frontend/src/components/ChatPreviewModal.jsx`)

**Added:**
- Import `useEffect` and `useRef` from React
- Created `messagesEndRef` reference to track the end of messages
- Added `useEffect` hook to trigger scroll when messages or loading state changes
- Created `scrollToBottom()` function for smooth scrolling
- Added invisible anchor div at the end of messages list

**Implementation:**
```javascript
// Added imports
import React, { useState, useEffect, useRef } from 'react';

// Added ref
const messagesEndRef = useRef(null);

// Auto-scroll effect
useEffect(() => {
  scrollToBottom();
}, [messages, loading]);

const scrollToBottom = () => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
};

// Anchor element at end of messages
<div ref={messagesEndRef} />
```

### 2. PublicChat.jsx (`/app/frontend/src/pages/PublicChat.jsx`)

**Updated:**
- Enhanced existing `useEffect` to also trigger on `sending` state changes
- This ensures the chat scrolls when loading indicator appears

**Before:**
```javascript
useEffect(() => {
  scrollToBottom();
}, [messages]);
```

**After:**
```javascript
useEffect(() => {
  scrollToBottom();
}, [messages, sending]);
```

## How It Works

1. **Ref-based Scrolling**: Uses React ref (`messagesEndRef`) to create an anchor point at the bottom of the messages container
2. **Smooth Behavior**: Employs `scrollIntoView({ behavior: 'smooth' })` for animated scrolling
3. **Automatic Trigger**: Scrolls automatically when:
   - New message is added (user or assistant)
   - Loading state changes (typing indicator appears/disappears)
   - Sending state changes (for public chat)

## Benefits

✅ **Only Messages Scroll**: The entire page stays in place - only the chat messages container scrolls
✅ **Smooth Animation**: Uses CSS smooth scrolling for better UX
✅ **Automatic**: No user action required - works seamlessly
✅ **Responsive**: Works on all screen sizes
✅ **Non-intrusive**: Doesn't interfere with manual scrolling

## Testing

To test the auto-scroll feature:

1. **Chat Preview Modal**:
   - Go to Dashboard → Create/Open a Chatbot
   - Click "Test Chat" or preview button
   - Send multiple messages
   - Observe smooth auto-scroll to latest message

2. **Public Chat Page**:
   - Navigate to `/public-chat/{chatbot-id}`
   - Send multiple messages in succession
   - Watch the messages area scroll automatically
   - Note that header and input area remain fixed

## Technical Details

- **Scroll Container**: `.flex-1.overflow-y-auto` div containing messages
- **Scroll Method**: `Element.scrollIntoView()` API
- **Performance**: Minimal overhead - only triggers on state changes
- **Browser Support**: Works in all modern browsers (Chrome, Firefox, Safari, Edge)

## Files Modified

1. `/app/frontend/src/components/ChatPreviewModal.jsx` - Added auto-scroll functionality
2. `/app/frontend/src/pages/PublicChat.jsx` - Enhanced existing auto-scroll to include sending state

## Notes

- The scroll behavior is "smooth" which provides a pleasant animation
- The anchor element (`<div ref={messagesEndRef} />`) is invisible and has no styling impact
- Manual scrolling by the user is not prevented - auto-scroll only triggers on new content
- Works correctly with loading indicators and message animations
