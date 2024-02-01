## Usage

[Helm](https://helm.sh) must be installed to use the charts.  Please refer to
Helm's [documentation](https://helm.sh/docs) to get started.

Once Helm has been set up correctly, add the repo as follows:
```bash
helm repo add canonical-storage https://canonical.github.io/rawfile-localpv
```
If you had already added this repo earlier, run `helm repo update` to retrieve
the latest versions of the packages.  You can then run `helm search repo
canonical-storage` to see the charts.

To install the `rawfile-localpv`` chart:

```bash
helm install my-rawfile-localpv canonical-storage/rawfile-localpv
```

To uninstall the chart:
```bash
helm delete my-rawfile-localpv
```
