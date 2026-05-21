
## API Canvas

Now that we have a basic idea of the API we're going to implement, we can start designing it.

The API Canvas is a simple tool to design APIs from different perspectives, and to keep track of the design decisions.
The basic idea is described in [The design of web APIs, by Arnaud Lauret](https://github.com/arno-di-loreto/design-of-web-apis-2e),
but in this course we will use a simplified version.

We'll start filling the following grid.

| Whos | Whats |Hows |Inputs |Outputs | Goals |
|------|-------|-----|------|-------|-------|
| Who are the users of the API? | What do they want to do? | How do they do it? | What data do they send? Where do they get it from? | What data do they get fro the API? How do they use it? | What are their goals? |

---

### Case Study: Defibrillators API

To make this concrete we will design a hypothetical API that allows
**citizens** to locate defibrillators (DAE) on a map and **institutions** to manage the device registry.

The canvas maps *who*, *what*, *how*, and *why* in order to:

1. Define the service and its use cases;
2. Identify resources and actions following a REST approach;
3. Describe resources and actions in OpenAPI 3.

**Catalog metadata:** *Title* — Defibrillators | *Subtitle* — Show defibrillators in an area and find the nearest one

| Whos                                                    | Whats                                                    | Hows                                                   | Inputs                                             | Outputs                                                                          | Goals                                                                     |
| ------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Private organisations                                   | Publish information about defibrillators in a given area | Map management tools                                   | Area ID determined by the requester                | List of defibrillators with GPS coordinates and status (available / unavailable) | Publish the registry on maps or display screens (hotels, buses, metro, …) |
| Open data / civic hackers / journalists / public bodies | Monitor DAE distribution across a territory              | Data-science tools: bulk download or dedicated clients | Area ID and timestamp, determined by the requester | List of defibrillators with GPS coordinates and status (available / unavailable) | Inform the public about defibrillator coverage; evaluate service coverage |
