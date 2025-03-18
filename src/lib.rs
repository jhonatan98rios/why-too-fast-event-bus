use pyo3::prelude::*;
use pyo3::types::{PyDict};
use tokio::sync::{mpsc, RwLock};
use tokio::runtime::Runtime;
use std::collections::HashMap;
use std::sync::Arc;

/// Struct for event bus
/// This struct represents an event bus that allows subscribing to events
/// with callbacks and publishing events with arguments.
#[pyclass]
struct WhyTooFastEventBus {
    /// A map of event names to lists of callback functions
    subscribers: Arc<RwLock<HashMap<String, Vec<PyObject>>>>,
    /// A sender for publishing events
    sender: mpsc::Sender<(String, PyObject)>,
    /// A Tokio runtime for managing asynchronous tasks
    runtime: Arc<Runtime>,
}

#[pymethods]
impl WhyTooFastEventBus {
    /// Creates a new WhyTooFastEventBus instance
    /// This function initializes the event bus, sets up the Tokio runtime,
    /// and spawns an asynchronous task to process events.
    #[new]
    fn new(_py: Python) -> PyResult<Self> {
        
        let subscribers = Arc::new(RwLock::new(HashMap::new()));
        let (sender, mut receiver): (mpsc::Sender<(String, PyObject)>, mpsc::Receiver<(String, PyObject)>) = mpsc::channel(1024);

        // Clone subscribers for async task
        let subs_clone = subscribers.clone();

        // Create a new Tokio runtime
        let runtime = Runtime::new().expect("Failed to create Tokio runtime");
        let runtime_handle = runtime.handle().clone();

        // Spawn the async event processing task
        runtime_handle.spawn(async move {
            // Process events as they arrive
            while let Some((event, args)) = receiver.recv().await {
                // Get the subscribers for the event
                let subs = subs_clone.read().await;
                // Call each callback with the arguments
                if let Some(callbacks) = subs.get(&event) {
                    let callbacks: &Vec<PyObject> = callbacks;
                    Python::with_gil(|py| {
                        for callback in callbacks {
                            let callback: &PyAny = callback.as_ref(py);
                            let _ = callback.call1((args.clone(),));
                        }
                    });
                }
            }
        });

        Ok(Self { subscribers, sender, runtime: Arc::new(runtime) })
    }

    /// Subscribe to an event with a callback
    /// This function allows you to subscribe to a specific event by providing
    /// an event name and a callback function. The callback will be called
    /// whenever the event is published.
    ///
    /// # Arguments
    /// * `event` - The name of the event to subscribe to
    /// * `callback` - The callback function to be called when the event is published
    fn subscribe(&self, event: String, callback: PyObject) -> PyResult<()> {
        let subscribers = self.subscribers.clone();
        let runtime_handle = self.runtime.handle().clone();
        
        // Schedule subscription modification within the runtime
        runtime_handle.block_on(async move {
            let mut subs = subscribers.write().await;
            subs.entry(event).or_insert_with(Vec::new).push(callback);
        });
    
        Ok(())
    }

    /// Publish an event with arguments3
    /// This function allows you to publish an event by providing an event name
    /// and a list of arguments. All subscribed callbacks for the event will be
    /// called with the provided arguments.
    /// 
    /// # Arguments
    ///
    /// * `event` - The name of the event to publish
    /// * `args` - A dict of arguments to pass to the callbacks
    fn publish(&self, py: Python, event: String, args: &PyDict) -> PyResult<()> {
        let args_obj = args.into_py(py);
        let sender = self.sender.clone();
        // Send event without spawning a new task (ensures order)
        let _ = sender.try_send((event, args_obj));
        Ok(())
    }
}

/// Register Rust module in Python
/// This function registers the `WhyTooFastEventBus` class in the Python module.
#[pymodule]
fn why_too_fast_event_bus_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WhyTooFastEventBus>()?;
    Ok(())
}